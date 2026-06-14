"""
AllToolkit 语言共振分析仪测试套件
"""

import unittest
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_resonator import (
    generate_resonance_report,
    get_resonance_only,
    _calc_resonance,
    _resonance_bar,
    _waveform,
    LANGUAGE_FREQUENCIES,
    next_lang,
)


# 测试用固定时间：2026-06-15 04:00（周一，凌晨）
_FIXED_TIME = datetime(2026, 6, 15, 4, 0, 0)

# 初始测试数据：current_index=0 → Rust
_INITIAL_TEST_DATA = {
    "languages": [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ],
    "current_index": 0,
    "last_language": "C/C++",
    "updated_at": "2026-06-14T03:00:00+08:00",
}


def _make_temp_json():
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_resonator_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(_INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
    return path


# ─────────────────────────────────────────────
# 语言频率映射完整性
# ─────────────────────────────────────────────

EXPECTED_LANGUAGES = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


class TestPolyglotResonator(unittest.TestCase):

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    # ── 语言频率映射 ─────────────────────────────

    def test_all_languages_have_frequency(self):
        """所有轮换语言都有频率映射"""
        for lang in EXPECTED_LANGUAGES:
            self.assertIn(lang, LANGUAGE_FREQUENCIES, f"{lang} 缺少频率映射")

    def test_frequencies_in_valid_range(self):
        """所有频率应在合理范围内（20~600 Hz 人文隐喻）"""
        for lang, freq in LANGUAGE_FREQUENCIES.items():
            self.assertGreaterEqual(freq, 20.0)
            self.assertLessEqual(freq, 600.0)

    # ── 共振计算 ─────────────────────────────────

    def test_resonance_returns_all_fields(self):
        """共振数据包含所有字段"""
        r = _calc_resonance("Rust", _FIXED_TIME)
        self.assertIn("raw", r)
        self.assertIn("hour_factor", r)
        self.assertIn("week_factor", r)
        self.assertIn("season_factor", r)
        self.assertIn("frequency", r)

    def test_resonance_values_in_range(self):
        """共振各因子在 0.0~1.0 区间"""
        for lang in EXPECTED_LANGUAGES:
            r = _calc_resonance(lang, _FIXED_TIME)
            self.assertGreaterEqual(r["raw"], 0.0)
            self.assertLessEqual(r["raw"], 1.0)
            self.assertGreaterEqual(r["hour_factor"], 0.0)
            self.assertLessEqual(r["hour_factor"], 1.0)
            self.assertGreaterEqual(r["week_factor"], 0.0)
            self.assertLessEqual(r["week_factor"], 1.0)
            self.assertGreaterEqual(r["season_factor"], 0.0)
            self.assertLessEqual(r["season_factor"], 1.0)

    def test_resonance_rust_at_4am(self):
        """凌晨 4 点 Rust 共振强度应较高（深夜精密时段）"""
        r = _calc_resonance("Rust", _FIXED_TIME)
        # 凌晨 4 点时段因子为 0.8，Rust 频率最低（27.5 Hz）
        # raw = (27.5/493.9) * 0.8 * week(周一0.8) * season(夏季~初秋0.8附近)
        self.assertGreater(r["raw"], 0.0)
        self.assertEqual(r["hour_factor"], 0.8)

    def test_resonance_typescript_at_10am(self):
        """上午 10 点 TypeScript 应有高共振"""
        morning = datetime(2026, 6, 15, 10, 0, 0)
        r = _calc_resonance("TypeScript", morning)
        self.assertEqual(r["hour_factor"], 1.0)
        self.assertGreater(r["raw"], 0.0)

    # ── next_lang ────────────────────────────────

    def test_next_lang_forward(self):
        """next_lang 按顺序前进"""
        order = ["Rust", "Go", "Swift", "Kotlin",
                 "TypeScript", "JavaScript", "Java", "C/C++"]
        for i, lang in enumerate(order):
            self.assertEqual(next_lang(lang), order[(i + 1) % len(order)])

    def test_next_lang_wrap_around(self):
        """C/C++ 之后回到 Rust"""
        self.assertEqual(next_lang("C/C++"), "Rust")

    def test_next_lang_unknown(self):
        """未知语言默认返回 Rust"""
        self.assertEqual(next_lang("Forth"), "Rust")

    # ── _resonance_bar ───────────────────────────

    def test_resonance_bar_length(self):
        """共振条总长度为 width + 1"""
        bar = _resonance_bar(0.5, max_val=1.0, width=30)
        self.assertEqual(len(bar), 30)

    def test_resonance_bar_full(self):
        """value == max_val 时全为 █"""
        bar = _resonance_bar(1.0, max_val=1.0, width=20)
        self.assertEqual(bar, "█" * 20)

    def test_resonance_bar_empty(self):
        """value == 0 时全为 ░"""
        bar = _resonance_bar(0.0, max_val=1.0, width=20)
        self.assertEqual(bar, "░" * 20)

    # ── _waveform ────────────────────────────────

    def test_waveform_returns_string(self):
        """波形返回字符串，非空"""
        wave = _waveform(440.0, 5, width=40, period=1.0)
        self.assertIsInstance(wave, str)
        self.assertGreater(len(wave), 0)

    def test_waveform_has_newlines(self):
        """波形包含换行符（多行图形）"""
        wave = _waveform(440.0, 5, width=40, period=2.0)
        self.assertIn("\n", wave)

    # ── generate_resonance_report ─────────────────

    def test_generate_returns_all_fields(self):
        """生成报告返回所有字段"""
        result = generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        for field in ["language", "next_language", "resonance", "wave_panel",
                      "report", "rank", "all_resonances", "json_updated", "timestamp"]:
            self.assertIn(field, result, f"缺少字段: {field}")

    def test_generate_current_language(self):
        """当前语言应为 Rust（index=0）"""
        result = generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(result["language"], "Rust")

    def test_generate_next_language(self):
        """下一个语言应为 Go"""
        result = generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(result["next_language"], "Go")

    def test_generate_updates_index(self):
        """生成后 JSON 的 current_index 应前进一位"""
        generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 1)
        self.assertEqual(data["last_language"], "Rust")

    def test_generate_updates_timestamp(self):
        """生成后 updated_at 应更新"""
        generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertNotEqual(data["updated_at"], _INITIAL_TEST_DATA["updated_at"])

    def test_generate_report_contains_language(self):
        """Markdown 报告包含语言名称"""
        result = generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertIn("Rust", result["report"])

    def test_generate_report_contains_resonance_value(self):
        """报告包含共振数值"""
        result = generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertIn("共振", result["report"])

    def test_generate_report_contains_wave_panel(self):
        """报告包含波形面板"""
        result = generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertIn("```", result["report"])

    def test_generate_all_resonances_all_languages(self):
        """全语言共振数据包含所有语言"""
        result = generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        for lang in EXPECTED_LANGUAGES:
            self.assertIn(lang, result["all_resonances"])

    def test_generate_rank_within_range(self):
        """排名在 1~8 之间"""
        result = generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertGreaterEqual(result["rank"], 1)
        self.assertLessEqual(result["rank"], len(EXPECTED_LANGUAGES))

    def test_generate_json_updated_true(self):
        """json_updated 标志应为 True"""
        result = generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertTrue(result["json_updated"])

    # ── get_resonance_only ───────────────────────

    def test_query_does_not_change_index(self):
        """查询共振（不推进）不应改变 current_index"""
        with open(self.test_path, "r", encoding="utf-8") as f:
            before = json.load(f)["current_index"]
        get_resonance_only(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            after = json.load(f)["current_index"]
        self.assertEqual(before, after)

    def test_query_returns_current_language(self):
        """不指定语言时查询当前语言（Rust）"""
        result = get_resonance_only(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(result["language"], "Rust")

    def test_query_specific_language(self):
        """指定语言时返回该语言的共振数据"""
        result = get_resonance_only(language="Go", json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(result["language"], "Go")
        self.assertIn("resonance", result)
        self.assertIn("rank", result)
        self.assertIn("all_resonances", result)

    # ── 轮换完整性 ───────────────────────────────

    def test_full_rotation_cycle(self):
        """完整轮换一圈（8 次），验证所有语言顺序正确"""
        # 重置到 Rust（index=0）
        with open(self.test_path, "w", encoding="utf-8") as f:
            json.dump(_INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)

        expected_order = ["Rust", "Go", "Swift", "Kotlin",
                          "TypeScript", "JavaScript", "Java", "C/C++"]
        for i, expected in enumerate(expected_order):
            result = generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
            self.assertEqual(
                result["language"], expected,
                f"第 {i+1} 次轮换期望 {expected}，实际 {result['language']}"
            )


class TestPolyglotResonatorIntegration(unittest.TestCase):

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_consecutive_rotations(self):
        """连续轮换两次，索引正确前移，JSON 同步"""
        r1 = generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(r1["language"], "Rust")
        self.assertEqual(r1["next_language"], "Go")

        r2 = generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(r2["language"], "Go")
        self.assertEqual(r2["next_language"], "Swift")

        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 2)

    def test_query_then_generate(self):
        """先查询不推进，再生成推进，状态正确"""
        q = get_resonance_only(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(q["language"], "Rust")

        with open(self.test_path, "r", encoding="utf-8") as f:
            idx_before = json.load(f)["current_index"]

        g = generate_resonance_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(g["language"], "Rust")  # 轮换前还是 Rust

        with open(self.test_path, "r", encoding="utf-8") as f:
            idx_after = json.load(f)["current_index"]

        self.assertEqual(idx_before, idx_after - 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)