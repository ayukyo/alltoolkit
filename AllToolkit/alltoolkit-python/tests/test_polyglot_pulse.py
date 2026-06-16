"""
test_polyglot_pulse.py — Polyglot Pulse 单元测试
====================================================================
测试目标：
  1. get_pulse_report() 读取 language_rotation.json，按 current_index 取语言
  2. 报告生成后，language_rotation.json 的 current_index 前移一位
  3. 脉搏率计算正确（指数衰减：exp(-hours/24)）
  4. 脉搏区间判断正确（blazing/hot/warm/cool/cold/frozen）
  5. 心电图（ecg_line）随脉搏率变化
  6. 活跃条（activity_bar）随脉搏率变化
  7. 推荐逻辑正确（刚练过→推荐次热，全部冷了→推荐最少练）
  8. get_pulse_preview() 不推进索引
  9. format_pulse_console() 格式正确
  10. format_pulse_markdown() 格式正确
  11. get_language_pulse() 查询指定语言
  12. 全语言排行正确
  13. 轮换一圈（8次）后回到原点

作者：AllToolkit 全自动生成
====================================================================
"""

import unittest
import unittest.mock
import json
import os
import sys
import tempfile
import math
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_pulse import (
    get_pulse_report,
    get_pulse_preview,
    get_language_pulse,
    format_pulse_console,
    format_pulse_markdown,
    _compute_pulse_data,
    _pulse_rate,
    _pulse_zone,
    _build_ecg_line,
    _build_activity_bar,
    _hours_ago,
    _collect_all_entries,
    CORE_LANGUAGES,
    LANGUAGE_EMOJI,
)


# ─────────────────────────────────────────────
# 测试数据
# ─────────────────────────────────────────────
_INITIAL_YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

INITIAL_ROTATION_DATA = {
    "languages": [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ],
    "current_index": 0,  # Rust
    "last_language": "C/C++",
    "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
}

# 固定测试时间：2026-06-15 10:00
_FIXED_TIME = datetime(2026, 6, 15, 10, 0, 0)


def _make_temp_json(data: dict = None) -> str:
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_pulse_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data or INITIAL_ROTATION_DATA, f, ensure_ascii=False, indent=2)
    return path


def _make_temp_log(name: str, entries: list) -> str:
    """创建临时日志文件。entries: [{'language': ..., 'timestamp': ...}]"""
    fd, path = tempfile.mkstemp(suffix=".json", prefix=f"test_pulse_{name}_")
    os.close(fd)
    data = {"attempts": entries, "total_katas": len(entries)}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


# ─────────────────────────────────────────────
# 测试用例
# ─────────────────────────────────────────────

class TestPulseHelpers(unittest.TestCase):
    """脉搏辅助函数测试"""

    def test_pulse_rate_exponential_decay(self):
        """脉搏率按指数衰减：0h=1.0, 24h≈0.368"""
        self.assertAlmostEqual(_pulse_rate(0), 1.0, places=5)
        self.assertAlmostEqual(_pulse_rate(24), math.exp(-1), places=5)
        self.assertAlmostEqual(_pulse_rate(48), math.exp(-2), places=5)
        self.assertAlmostEqual(_pulse_rate(0), 1.0, places=5)

    def test_pulse_rate_decreases_with_time(self):
        """脉搏率随时间单调递减"""
        r0 = _pulse_rate(0)
        r6 = _pulse_rate(6)
        r24 = _pulse_rate(24)
        r72 = _pulse_rate(72)
        self.assertGreater(r0, r6)
        self.assertGreater(r6, r24)
        self.assertGreater(r24, r72)

    def test_pulse_zone_blazing(self):
        """≤2小时：炽热"""
        self.assertEqual(_pulse_zone(0.5), "🔥 炽热")
        self.assertEqual(_pulse_zone(2), "🔥 炽热")

    def test_pulse_zone_hot(self):
        """2~6小时：活跃"""
        self.assertEqual(_pulse_zone(3), "⚡ 活跃")
        self.assertEqual(_pulse_zone(6), "⚡ 活跃")

    def test_pulse_zone_warm(self):
        """6~24小时：温热"""
        self.assertEqual(_pulse_zone(12), "🌡️ 温热")
        self.assertEqual(_pulse_zone(24), "🌡️ 温热")

    def test_pulse_zone_cool(self):
        """24~72小时：冷却"""
        self.assertEqual(_pulse_zone(48), "🧊 冷却")
        self.assertEqual(_pulse_zone(72), "🧊 冷却")

    def test_pulse_zone_cold(self):
        """72~168小时：寒冷"""
        self.assertEqual(_pulse_zone(100), "❄️ 寒冷")
        self.assertEqual(_pulse_zone(168), "❄️ 寒冷")

    def test_pulse_zone_frozen(self):
        """>168小时：冻结"""
        self.assertEqual(_pulse_zone(200), "💀 冻结")
        self.assertEqual(_pulse_zone(9999), "💀 冻结")

    def test_ecg_line_high_rate(self):
        """高脉搏率（>0.7）生成完整心电图"""
        line = _build_ecg_line(0.9)
        self.assertEqual(len(line), 50)
        # 高心率生成完整波形，包含多种字符（非单一字符）
        unique_chars = set(line)
        self.assertGreater(len(unique_chars), 3,
            f"High rate ECG should have diverse chars, got: {line}")

    def test_ecg_line_low_rate(self):
        """低脉搏率生成微弱心电图"""
        line = _build_ecg_line(0.1)
        self.assertEqual(len(line), 50)
        # 低心率生成微弱波形
        self.assertGreater(len(line), 0)

    def test_ecg_line_zero_rate(self):
        """零脉搏率生成全平线"""
        line = _build_ecg_line(0.0)
        self.assertEqual(len(line), 50)
        self.assertTrue(all(c == "░" for c in line))

    def test_activity_bar_high(self):
        """高脉搏率生成满格条"""
        bar = _build_activity_bar(0.9)
        self.assertEqual(len(bar), 20)
        self.assertTrue(bar.startswith("█"))

    def test_activity_bar_low(self):
        """低脉搏率生成空格条"""
        bar = _build_activity_bar(0.1)
        self.assertEqual(len(bar), 20)
        self.assertTrue(bar.startswith("░"))

    def test_hours_ago_calculation(self):
        """距今小时数计算正确"""
        now = datetime(2026, 6, 15, 10, 0, 0)
        past = datetime(2026, 6, 15, 4, 0, 0)
        self.assertAlmostEqual(_hours_ago(past, now), 6.0, places=2)

        past2 = datetime(2026, 6, 14, 10, 0, 0)
        self.assertAlmostEqual(_hours_ago(past2, now), 24.0, places=2)


class TestPulseReport(unittest.TestCase):
    """脉搏报告主 API 测试"""

    def setUp(self):
        self.test_path = _make_temp_json()
        self.rot_path = self.test_path  # same for report

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_report_returns_all_required_fields(self):
        """报告返回所有必要字段"""
        result = get_pulse_report(json_path=self.test_path, now=_FIXED_TIME)
        required = [
            "current_language", "next_language", "pulse_data",
            "rankings", "recommended_language", "recommended_reason",
            "json_updated", "timestamp",
        ]
        for field in required:
            self.assertIn(field, result, f"Missing field: {field}")

    def test_report_current_language(self):
        """当前语言为 Rust（index=0）"""
        result = get_pulse_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(result["current_language"], "Rust")

    def test_report_next_language(self):
        """下一个语言为 Go"""
        result = get_pulse_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(result["next_language"], "Go")

    def test_report_pulse_data_has_all_languages(self):
        """pulse_data 包含所有 8 种语言"""
        result = get_pulse_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(len(result["pulse_data"]), 8)
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, result["pulse_data"])

    def test_report_pulse_data_fields(self):
        """每种语言的脉搏数据包含必要字段"""
        result = get_pulse_report(json_path=self.test_path, now=_FIXED_TIME)
        for lang, pd in result["pulse_data"].items():
            required = [
                "language", "emoji", "pulse_rate", "pulse_zone",
                "hours_since_last", "total_sessions", "last_practiced",
                "activity_bar", "ecg_line", "daily_intensity",
                "streak_days", "recommendation_score",
            ]
            for field in required:
                self.assertIn(field, pd, f"{lang}: missing {field}")

    def test_report_rankings_sorted(self):
        """脉搏排行榜按脉搏率降序排列"""
        result = get_pulse_report(json_path=self.test_path, now=_FIXED_TIME)
        rates = [rate for _, rate in result["rankings"]]
        self.assertEqual(rates, sorted(rates, reverse=True))

    def test_report_json_advances_index(self):
        """报告生成后，current_index 前移一位"""
        get_pulse_report(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 1)  # Rust(0) → Go(1)

    def test_report_json_updates_timestamp(self):
        """报告生成后，updated_at 更新"""
        with open(self.test_path, "r", encoding="utf-8") as f:
            before = json.load(f)["updated_at"]
        get_pulse_report(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            after = json.load(f)["updated_at"]
        self.assertNotEqual(before, after)

    def test_report_json_records_last_language(self):
        """last_language 记录上一轮换的语言"""
        get_pulse_report(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["last_language"], "Rust")


class TestPulsePreview(unittest.TestCase):
    """脉搏预览（不推进索引）测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_preview_does_not_advance_index(self):
        """预览不改变 current_index"""
        with open(self.test_path, "r", encoding="utf-8") as f:
            before = json.load(f)["current_index"]
        get_pulse_preview(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            after = json.load(f)["current_index"]
        self.assertEqual(before, after)

    def test_preview_returns_correct_fields(self):
        """预览返回正确字段"""
        result = get_pulse_preview(json_path=self.test_path, now=_FIXED_TIME)
        self.assertIn("current_language", result)
        self.assertIn("pulse_data", result)
        self.assertIn("rankings", result)
        self.assertIn("timestamp", result)


class TestFormatPulseConsole(unittest.TestCase):
    """控制台格式化测试"""

    def test_console_format_contains_language(self):
        """格式输出包含语言名称"""
        result = get_pulse_report(now=_FIXED_TIME)
        output = format_pulse_console(result)
        self.assertIn("Polyglot Pulse", output)
        self.assertIn("Rust", output)
        self.assertIn("Go", output)

    def test_console_format_contains_pulse_zones(self):
        """格式输出包含脉搏状态"""
        result = get_pulse_report(now=_FIXED_TIME)
        output = format_pulse_console(result)
        # 至少包含一个脉搏区间标签
        found = any(
            zone in output
            for zone in ["炽热", "活跃", "温热", "冷却", "寒冷", "冻结"]
        )
        self.assertTrue(found)

    def test_console_format_contains_recommendation(self):
        """格式输出包含推荐信息"""
        result = get_pulse_report(now=_FIXED_TIME)
        output = format_pulse_console(result)
        self.assertIn("推荐", output)
        self.assertIn(result["recommended_language"], output)


class TestFormatPulseMarkdown(unittest.TestCase):
    """Markdown 格式化测试"""

    def test_markdown_format_contains_language(self):
        """Markdown 输出包含语言名称"""
        result = get_pulse_report(now=_FIXED_TIME)
        output = format_pulse_markdown(result)
        self.assertIn("语言脉搏监测报告", output)
        self.assertIn("Rust", output)

    def test_markdown_format_contains_rankings(self):
        """Markdown 输出包含排行榜"""
        result = get_pulse_report(now=_FIXED_TIME)
        output = format_pulse_markdown(result)
        self.assertIn("脉搏排行榜", output)
        self.assertIn("推荐", output)


class TestGetLanguagePulse(unittest.TestCase):
    """指定语言脉搏查询测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_get_language_pulse_rust(self):
        """查询 Rust 脉搏数据"""
        result = get_language_pulse("Rust", json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(result["language"], "Rust")
        self.assertIn("pulse_rate", result)
        self.assertIn("pulse_zone", result)
        self.assertIn("ecg_line", result)
        self.assertIn("activity_bar", result)
        self.assertIn("daily_intensity_chart", result)

    def test_get_language_pulse_all_core(self):
        """所有核心语言都能查询"""
        for lang in CORE_LANGUAGES:
            result = get_language_pulse(lang, json_path=self.test_path, now=_FIXED_TIME)
            self.assertEqual(result["language"], lang)

    def test_get_language_pulse_invalid_raises(self):
        """无效语言抛出 ValueError"""
        with self.assertRaises(ValueError):
            get_language_pulse("Python", json_path=self.test_path, now=_FIXED_TIME)


class TestPulseWithHistory(unittest.TestCase):
    """有历史记录时的脉搏计算测试"""

    def setUp(self):
        self.test_path = _make_temp_json()
        self.now_str = _FIXED_TIME.strftime("%Y-%m-%dT%H:%M:%S+08:00")
        self.yesterday_str = (_FIXED_TIME - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S+08:00")
        self.week_ago_str = (_FIXED_TIME - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S+08:00")

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_pulse_without_history(self):
        """无历史记录时脉搏率为 0"""
        # Patch _collect_all_entries to return empty entries
        with unittest.mock.patch(
            "modules.polyglot_pulse._collect_all_entries",
            return_value={lang: [] for lang in CORE_LANGUAGES},
        ):
            result = get_pulse_preview(json_path=self.test_path, now=_FIXED_TIME)

        # 所有语言脉搏率为 0
        for lang, pd in result["pulse_data"].items():
            self.assertEqual(pd["pulse_rate"], 0.0)
            self.assertEqual(pd["total_sessions"], 0)
            self.assertEqual(pd["pulse_zone"], "💀 冻结")

    def test_pulse_rate_with_history_calculated(self):
        """有历史记录时脉搏率按指数衰减计算"""
        # 直接测试 _compute_pulse_data，验证 Rust 30分钟前练习时脉搏率 ≈ 0.98
        recent_time = _FIXED_TIME - timedelta(minutes=30)
        recent_dt = recent_time

        entries = {
            "Rust": [recent_dt],  # 30分钟前练习过 Rust
        }

        pulse_data = _compute_pulse_data(entries, _FIXED_TIME)

        rust_rate = pulse_data["Rust"]["pulse_rate"]
        # 30分钟前 → rate ≈ exp(-0.5/24) ≈ 0.979
        self.assertAlmostEqual(rust_rate, math.exp(-0.5/24), places=3)
        self.assertGreater(rust_rate, 0.97)
        self.assertLess(rust_rate, 1.0)


class TestPulseRotationCycle(unittest.TestCase):
    """完整轮换一圈测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_full_rotation_cycle(self):
        """8 次轮换后回到 Rust"""
        languages_seen = []
        for i in range(8):
            result = get_pulse_report(json_path=self.test_path, now=_FIXED_TIME)
            languages_seen.append(result["current_language"])

        expected = ["Rust", "Go", "Swift", "Kotlin",
                    "TypeScript", "JavaScript", "Java", "C/C++"]
        self.assertEqual(languages_seen, expected)

    def test_no_repeated_language_in_one_cycle(self):
        """一轮（8次）中每种语言只出现一次"""
        languages_seen = []
        for i in range(8):
            result = get_pulse_report(json_path=self.test_path, now=_FIXED_TIME)
            languages_seen.append(result["current_language"])

        self.assertEqual(len(set(languages_seen)), 8)


class TestPulseEmojiAndCore(unittest.TestCase):
    """emoji 和核心语言常量测试"""

    def test_core_languages_count(self):
        """核心语言有 8 种"""
        self.assertEqual(len(CORE_LANGUAGES), 8)

    def test_core_languages_order(self):
        """核心语言顺序正确"""
        expected = ["Rust", "Go", "Swift", "Kotlin",
                    "TypeScript", "JavaScript", "Java", "C/C++"]
        self.assertEqual(CORE_LANGUAGES, expected)

    def test_all_core_languages_have_emoji(self):
        """所有核心语言都有 emoji 映射"""
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, LANGUAGE_EMOJI, f"{lang} missing emoji")
            self.assertTrue(len(LANGUAGE_EMOJI[lang]) <= 4, f"{lang} emoji too long")


if __name__ == "__main__":
    unittest.main(verbosity=2)
