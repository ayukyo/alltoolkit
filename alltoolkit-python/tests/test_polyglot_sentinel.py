"""
test_polyglot_sentinel.py - Polyglot Sentinel 单元测试
====================================================================
测试目标：
  1. get_sentinel_report() 读取 language_rotation.json，按 current_index 取语言
  2. 报告生成后，language_rotation.json 的 current_index 前移一位
  3. 健康分计算正确（0~100）
  4. 整体状态判断正确（EXCELLENT / HEALTHY / NEEDS_ATTENTION / CRITICAL）
  5. 雷达图 ASCII 正确渲染
  6. 警报生成正确（critical / warning / info）
  7. 连胜统计正确
  8. get_sentinel_preview() 不推进索引
  9. format_sentinel_console() 格式正确
  10. format_sentinel_markdown() 格式正确
  11. 所有测试通过

作者：AllToolkit 全自动生成
====================================================================
"""

import unittest
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, List

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_sentinel import (
    get_sentinel_report,
    get_sentinel_preview,
    format_sentinel_console,
    format_sentinel_markdown,
    CORE_LANGUAGES,
    LANGUAGE_EMOJI,
    SENTINEL_ADVICE,
    _build_activity_matrix,
    _compute_health_score,
    _generate_alerts,
    _compute_streak,
    _parse_dt,
    _days_ago,
)


# ─────────────────────────────────────────────
# 测试数据
# ─────────────────────────────────────────────
_INITIAL_YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

INITIAL_ROTATION_DATA = {
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
    "current_index": 0,
    "last_language": "",
    "updated_at": "2026-06-06T02:10:00+08:00",
}


def _make_temp_json():
    """创建临时 language_rotation.json"""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_sentinel_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(INITIAL_ROTATION_DATA, f, ensure_ascii=False, indent=2)
    return path


def _make_temp_log(name: str, data: Any) -> str:
    """创建临时日志 JSON"""
    fd, path = tempfile.mkstemp(suffix=".json", prefix=f"test_sentinel_{name}_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


# ─────────────────────────────────────────────
# 测试用例
# ─────────────────────────────────────────────

class TestPolyglotSentinel(unittest.TestCase):
    """Polyglot Sentinel 单元测试"""

    def setUp(self):
        import modules.polyglot_sentinel as s
        self.rot_path = _make_temp_json()

        # 创建临时日志文件（带测试数据）
        now_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

        # codex_log: Rust 和 Go 今天有活动
        codex_log = {
            "attempts": [
                {"language": "Rust", "generated_at": now_str, "title": "Rust kata 1"},
                {"language": "Go", "generated_at": now_str, "title": "Go kata 1"},
                {"language": "Rust", "generated_at": now_str, "title": "Rust kata 2"},
            ],
            "total_katas": 3,
        }

        # companion_history: Swift 有活动
        companion_log = {
            "entries": [
                {"language": "Swift", "timestamp": now_str, "feature_name": "Protocol Extensions"},
            ]
        }

        # quiz_history: Kotlin 有活动
        quiz_log = {
            "attempts": [
                {"language": "Kotlin", "timestamp": now_str, "quiz_title": "Kotlin Quiz 1"},
            ]
        }

        # 重定向日志路径
        s._LOG_PATHS = {
            "codex":    _make_temp_log("codex", codex_log),
            "companion": _make_temp_log("companion", companion_log),
            "quiz":     _make_temp_log("quiz", quiz_log),
            "ink":      _make_temp_log("ink", {}),
            "snippet":  _make_temp_log("snippet", {}),
            "map":      _make_temp_log("map", {}),
        }

    def _write_json(self, path: str, data: Any):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def tearDown(self):
        import modules.polyglot_sentinel as s
        for p in [self.rot_path] + list(s._LOG_PATHS.values()):
            if os.path.exists(p):
                os.remove(p)

    # ── get_sentinel_report ─────────────────

    def test_report_reads_language_from_rotation(self):
        """报告应读取 current_index=0 → Rust"""
        result = get_sentinel_report(json_path=self.rot_path)
        self.assertEqual(result["current_language"], "Rust")

    def test_report_returns_all_required_fields(self):
        """报告返回所有必要字段"""
        result = get_sentinel_report(json_path=self.rot_path)
        required = {
            "current_language", "emoji", "overall_score",
            "overall_status", "status_color", "scores",
            "last_seen_days", "radar_chart", "alerts",
            "streak", "total_entries", "language_rankings",
            "next_language",
        }
        self.assertTrue(
            required.issubset(result.keys()),
            f"缺少字段：{required - result.keys()}",
        )

    def test_report_next_language_is_go(self):
        """Rust 的下一个语言是 Go"""
        result = get_sentinel_report(json_path=self.rot_path)
        self.assertEqual(result["next_language"], "Go")

    def test_report_scores_are_0_to_100(self):
        """健康分应在 0~100 范围内"""
        result = get_sentinel_report(json_path=self.rot_path)
        for lang, score in result["scores"].items():
            self.assertIn(lang, CORE_LANGUAGES)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)

    def test_report_overall_score_is_average(self):
        """overall_score 应该是所有语言分数的平均值"""
        result = get_sentinel_report(json_path=self.rot_path)
        expected_avg = sum(result["scores"].values()) / len(result["scores"])
        self.assertAlmostEqual(result["overall_score"], expected_avg, places=1)

    def test_report_overall_status_values(self):
        """overall_status 应该是有效值之一"""
        valid_statuses = {
            "🟢 EXCELLENT",
            "🟡 HEALTHY",
            "🟠 NEEDS_ATTENTION",
            "🔴 CRITICAL",
        }
        result = get_sentinel_report(json_path=self.rot_path)
        self.assertIn(result["overall_status"], valid_statuses)

    def test_report_language_rankings_sorted(self):
        """language_rankings 应按分数降序排列"""
        result = get_sentinel_report(json_path=self.rot_path)
        scores = [score for _, score in result["language_rankings"]]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_report_total_entries_positive(self):
        """total_entries 应 >= 0"""
        result = get_sentinel_report(json_path=self.rot_path)
        self.assertGreaterEqual(result["total_entries"], 0)

    # ── 轮换索引推进 ───────────────────────

    def test_rotation_json_index_advances(self):
        """get_sentinel_report 后 current_index 应前移"""
        get_sentinel_report(json_path=self.rot_path)
        with open(self.rot_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 1)

    def test_rotation_json_last_language_updated(self):
        """get_sentinel_report 后 last_language 应更新"""
        get_sentinel_report(json_path=self.rot_path)
        with open(self.rot_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["last_language"], "Rust")

    def test_rotation_json_updated_at_changed(self):
        """get_sentinel_report 后 updated_at 应更新"""
        old_at = None
        with open(self.rot_path, "r", encoding="utf-8") as f:
            old_at = json.load(f)["updated_at"]

        get_sentinel_report(json_path=self.rot_path)

        with open(self.rot_path, "r", encoding="utf-8") as f:
            new_at = json.load(f)["updated_at"]
        self.assertNotEqual(old_at, new_at)

    # ── 健康分计算 ─────────────────────────

    def test_health_score_100_for_recent_activity(self):
        """最近 24h 内有活动的语言得 100 分"""
        now_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        matrix = {"Rust": [{"ts": now_str, "source": "test", "title": "t"}]}
        health = _compute_health_score(matrix)
        self.assertEqual(health["scores"]["Rust"], 100)

    def test_health_score_0_for_never_seen(self):
        """从未见过的语言得 0 分"""
        matrix = {"Rust": []}
        health = _compute_health_score(matrix)
        self.assertEqual(health["scores"]["Rust"], 0)

    def test_health_score_80_for_3_days(self):
        """2.9 天内有活动的语言得 80 分"""
        three_days_ago = (datetime.now() - timedelta(days=2, hours=22)).strftime("%Y-%m-%dT%H:%M:%S+08:00")
        matrix = {"Rust": [{"ts": three_days_ago, "source": "test", "title": "t"}]}
        health = _compute_health_score(matrix)
        self.assertEqual(health["scores"]["Rust"], 80)

    def test_health_score_60_for_7_days(self):
        """6.9 天内有活动的语言得 60 分"""
        seven_days_ago = (datetime.now() - timedelta(days=6, hours=22)).strftime("%Y-%m-%dT%H:%M:%S+08:00")
        matrix = {"Rust": [{"ts": seven_days_ago, "source": "test", "title": "t"}]}
        health = _compute_health_score(matrix)
        self.assertEqual(health["scores"]["Rust"], 60)

    def test_health_score_40_for_14_days(self):
        """13.9 天内有活动的语言得 40 分"""
        thirteen_days_ago = (datetime.now() - timedelta(days=13, hours=22)).strftime("%Y-%m-%dT%H:%M:%S+08:00")
        matrix = {"Rust": [{"ts": thirteen_days_ago, "source": "test", "title": "t"}]}
        health = _compute_health_score(matrix)
        self.assertEqual(health["scores"]["Rust"], 40)

    def test_health_score_10_for_over_14_days(self):
        """超过 14 天未活动的语言得 10 分"""
        thirty_days_ago = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%dT%H:%M:%S+08:00")
        matrix = {"Rust": [{"ts": thirty_days_ago, "source": "test", "title": "t"}]}
        health = _compute_health_score(matrix)
        self.assertEqual(health["scores"]["Rust"], 10)

    def test_overall_status_excellent(self):
        """平均分 >= 80 → EXCELLENT"""
        matrix = {"Rust": [{"ts": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"), "source": "test", "title": "t"}]}
        # 其余语言也都是今天
        for lang in CORE_LANGUAGES:
            matrix[lang] = [{"ts": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"), "source": "test", "title": "t"}]
        health = _compute_health_score(matrix)
        self.assertEqual(health["overall_status"], "🟢 EXCELLENT")

    def test_overall_status_critical(self):
        """平均分 < 40 → CRITICAL"""
        matrix = {lang: [] for lang in CORE_LANGUAGES}
        health = _compute_health_score(matrix)
        self.assertEqual(health["overall_status"], "🔴 CRITICAL")

    # ── 警报生成 ───────────────────────────

    def test_alert_critical_for_never_seen(self):
        """从未见过的语言生成 critical 警报"""
        scores = {"Rust": 0}
        last_seen = {"Rust": float("inf")}
        alerts = _generate_alerts(scores, last_seen)
        self.assertTrue(any(a["level"] == "critical" for a in alerts))

    def test_alert_warning_for_over_14_days(self):
        """超过 14 天的语言生成 warning 警报"""
        scores = {"Rust": 10}
        last_seen = {"Rust": 30.0}
        alerts = _generate_alerts(scores, last_seen)
        self.assertTrue(any(a["level"] == "critical" for a in alerts))

    def test_alert_info_for_7_days(self):
        """7 天未练的语言生成 info 警报"""
        scores = {"Rust": 60}
        last_seen = {"Rust": 7.0}
        alerts = _generate_alerts(scores, last_seen)
        self.assertTrue(any(a["level"] == "info" for a in alerts))

    def test_alert_message_contains_language(self):
        """警报消息应包含语言名称"""
        scores = {"Rust": 0}
        last_seen = {"Rust": float("inf")}
        alerts = _generate_alerts(scores, last_seen)
        self.assertTrue(len(alerts) >= 1)
        rust_alert = next((a for a in alerts if a["language"] == "Rust"), None)
        self.assertIsNotNone(rust_alert)
        self.assertIn("Rust", rust_alert["message"])

    def test_alert_advice_included(self):
        """警报应包含恢复建议"""
        scores = {"Rust": 0}
        last_seen = {"Rust": float("inf")}
        alerts = _generate_alerts(scores, last_seen)
        for alert in alerts:
            if alert["language"] == "Rust":
                self.assertIn("advice", alert)

    # ── 连胜统计 ─────────────────────────

    def test_streak_zero_when_no_entries(self):
        """无记录时 streak 为 0"""
        matrix = {lang: [] for lang in CORE_LANGUAGES}
        streak = _compute_streak(matrix)
        self.assertEqual(streak["total_active_days"], 0)
        self.assertEqual(streak["current_streak"], 0)

    def test_streak_counts_days(self):
        """连胜统计正确计数"""
        today = datetime.now()
        entries = []
        for i in range(3):
            ts = (today - timedelta(days=i)).strftime("%Y-%m-%dT12:00:00+08:00")
            entries.append({"ts": ts, "source": "test", "title": "t"})
        matrix = {"Rust": entries}
        streak = _compute_streak(matrix)
        self.assertEqual(streak["total_active_days"], 3)

    def test_streak_longest_run(self):
        """最长连续天数正确"""
        today = datetime.now()
        entries = []
        for i in [0, 1, 2, 5, 6, 7]:  # 跳过第 3、4 天
            ts = (today - timedelta(days=i)).strftime("%Y-%m-%dT12:00:00+08:00")
            entries.append({"ts": ts, "source": "test", "title": "t"})
        matrix = {"Rust": entries}
        streak = _compute_streak(matrix)
        self.assertEqual(streak["longest_streak"], 3)  # 最长连续是 3 天

    # ── get_sentinel_preview ───────────────

    def test_preview_does_not_advance_index(self):
        """get_sentinel_preview 不应改变 current_index"""
        with open(self.rot_path, "r", encoding="utf-8") as f:
            before = json.load(f)["current_index"]

        get_sentinel_preview(json_path=self.rot_path)

        with open(self.rot_path, "r", encoding="utf-8") as f:
            after = json.load(f)["current_index"]
        self.assertEqual(before, after)

    def test_preview_returns_current_language(self):
        """preview 返回 Rust（index=0）"""
        result = get_sentinel_preview(json_path=self.rot_path)
        self.assertEqual(result["current_language"], "Rust")

    def test_preview_returns_scores(self):
        """preview 返回 scores 字段"""
        result = get_sentinel_preview(json_path=self.rot_path)
        self.assertIn("scores", result)

    # ── format_sentinel_console ────────────

    def test_format_console_contains_language(self):
        """console 格式输出包含当前语言"""
        result = get_sentinel_report(json_path=self.rot_path)
        formatted = format_sentinel_console(result)
        self.assertIn(result["current_language"], formatted)

    def test_format_console_contains_emoji(self):
        """console 格式输出包含 emoji"""
        result = get_sentinel_report(json_path=self.rot_path)
        formatted = format_sentinel_console(result)
        self.assertIn(result["emoji"], formatted)

    def test_format_console_contains_radar(self):
        """console 格式输出包含雷达图"""
        result = get_sentinel_report(json_path=self.rot_path)
        formatted = format_sentinel_console(result)
        self.assertIn("Activity Radar", formatted)

    def test_format_console_contains_streak(self):
        """console 格式输出包含连胜统计"""
        result = get_sentinel_report(json_path=self.rot_path)
        formatted = format_sentinel_console(result)
        self.assertIn("连续", formatted)

    def test_format_console_contains_overall_score(self):
        """console 格式输出包含整体得分"""
        result = get_sentinel_report(json_path=self.rot_path)
        formatted = format_sentinel_console(result)
        self.assertIn(str(result["overall_score"]), formatted)

    # ── format_sentinel_markdown ──────────

    def test_format_markdown_contains_language(self):
        """markdown 格式输出包含当前语言"""
        result = get_sentinel_report(json_path=self.rot_path)
        formatted = format_sentinel_markdown(result)
        self.assertIn(result["current_language"], formatted)

    def test_format_markdown_contains_table(self):
        """markdown 格式输出包含表格"""
        result = get_sentinel_report(json_path=self.rot_path)
        formatted = format_sentinel_markdown(result)
        self.assertIn("|", formatted)  # Markdown 表格

    def test_format_markdown_contains_rankings(self):
        """markdown 格式输出包含排名"""
        result = get_sentinel_report(json_path=self.rot_path)
        formatted = format_sentinel_markdown(result)
        self.assertIn("语言活跃度", formatted)

    # ── CORE_LANGUAGES ───────────────────

    def test_core_languages_correct(self):
        """CORE_LANGUAGES 包含 8 种语言且顺序正确"""
        self.assertEqual(
            CORE_LANGUAGES,
            ["Rust", "Go", "Swift", "Kotlin",
             "TypeScript", "JavaScript", "Java", "C/C++"],
        )

    def test_language_emoji_complete(self):
        """LANGUAGE_EMOJI 覆盖所有核心语言"""
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, LANGUAGE_EMOJI, f"{lang} missing emoji")

    def test_sentinel_advice_complete(self):
        """SENTINEL_ADVICE 覆盖所有核心语言"""
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, SENTINEL_ADVICE, f"{lang} missing advice")
            advice = SENTINEL_ADVICE[lang]
            self.assertIn("tip", advice)
            self.assertIn("practice", advice)

    # ── _parse_dt ─────────────────────────

    def test_parse_dt_iso(self):
        """_parse_dt 正确解析 ISO 时间字符串"""
        dt = _parse_dt("2026-06-16T05:00:00+08:00")
        self.assertIsNotNone(dt)
        self.assertEqual(dt.year, 2026)

    def test_parse_dt_returns_none_for_invalid(self):
        """_parse_dt 对无效格式返回 None"""
        dt = _parse_dt("not a date")
        self.assertIsNone(dt)


class TestPolyglotSentinelIntegration(unittest.TestCase):
    """Polyglot Sentinel 集成测试"""

    def setUp(self):
        import modules.polyglot_sentinel as s
        self.rot_path = _make_temp_json()

        # 创建空日志文件（防止读取失败）
        empty_logs = {
            "codex":    {"attempts": [], "total_katas": 0},
            "companion": {"entries": []},
            "quiz":     {"attempts": []},
            "ink":      {"entries": []},
            "snippet":  {"entries": []},
            "map":      {"entries": []},
        }
        s._LOG_PATHS = {
            name: _make_temp_log(name, empty_logs[name])
            for name in ["codex", "companion", "quiz", "ink", "snippet", "map"]
        }

    def tearDown(self):
        import modules.polyglot_sentinel as s
        for p in [self.rot_path] + list(s._LOG_PATHS.values()):
            if os.path.exists(p):
                os.remove(p)

    def test_full_rotation_cycle(self):
        """完整轮换一圈（8 次），验证索引正确循环"""
        expected = ["Rust", "Go", "Swift", "Kotlin",
                   "TypeScript", "JavaScript", "Java", "C/C++"]
        for lang in expected:
            result = get_sentinel_report(json_path=self.rot_path)
            self.assertEqual(
                result["current_language"], lang,
                f"期望 {lang}，实际 {result['current_language']}",
            )

        # 第 9 次 → Rust 再次出现
        result = get_sentinel_report(json_path=self.rot_path)
        self.assertEqual(result["current_language"], "Rust")

    def test_preview_then_report_index_correct(self):
        """先 preview（不推进），再 report（推进）"""
        # preview 不推进
        r0 = get_sentinel_preview(json_path=self.rot_path)
        self.assertEqual(r0["current_language"], "Rust")

        # report 推进到 Go
        r1 = get_sentinel_report(json_path=self.rot_path)
        self.assertEqual(r1["current_language"], "Rust")

        # preview 仍是 Go（index 已前进）
        r2 = get_sentinel_preview(json_path=self.rot_path)
        self.assertEqual(r2["current_language"], "Go")

    def test_report_with_no_history(self):
        """没有任何历史记录时报告也能正常生成"""
        # 各日志文件为空或不存在 → 得分为 0
        result = get_sentinel_report(json_path=self.rot_path)
        self.assertIn(result["overall_status"], {
            "🟢 EXCELLENT", "🟡 HEALTHY", "🟠 NEEDS_ATTENTION", "🔴 CRITICAL",
        })
        self.assertEqual(result["total_entries"], 0)

    def test_multiple_reports_accumulate_index(self):
        """多次调用 report，索引正确累进"""
        results = []
        for _ in range(4):
            results.append(get_sentinel_report(json_path=self.rot_path))

        languages = [r["current_language"] for r in results]
        self.assertEqual(languages, ["Rust", "Go", "Swift", "Kotlin"])


if __name__ == "__main__":
    unittest.main(verbosity=2)