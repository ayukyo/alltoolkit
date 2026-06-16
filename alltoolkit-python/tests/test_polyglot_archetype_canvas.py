"""
AllToolkit 语言原神殿堂测试套件
"""

import unittest
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_archetype_canvas import (
    generate_archetype_report,
    get_archetype_only,
    _calc_daily_state,
    _hour_to_vitality,
    _hour_to_creativity,
    _hour_to_focus,
    _hour_to_social,
    _time_to_mood,
    _fortune_rating,
    _build_stat_bar,
    _attribute_rating,
    _generate_ascii_portrait,
    LANGUAGE_ARCHETYPES,
    ALL_LANGUAGES,
    next_lang,
)


# 测试用固定时间：2026-06-15 10:00（周一，上午黄金期）
_FIXED_TIME = datetime(2026, 6, 15, 10, 0, 0)

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

EXPECTED_LANGUAGES = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


def _make_temp_json(initial_data=None):
    if initial_data is None:
        initial_data = _INITIAL_TEST_DATA
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_archetype_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(initial_data, f, ensure_ascii=False, indent=2)
    return path


# ─────────────────────────────────────────────
# 语言原型映射完整性
# ─────────────────────────────────────────────

class TestArchetypeMapping(unittest.TestCase):

    def test_all_languages_have_archetype(self):
        """所有轮换语言都有原型映射"""
        for lang in EXPECTED_LANGUAGES:
            self.assertIn(lang, LANGUAGE_ARCHETYPES, f"{lang} 缺少原型映射")

    def test_all_archetypes_have_required_fields(self):
        """每个原型都包含所有必需字段"""
        required = ["archetype", "element", "domain", "personality",
                    "strengths", "weaknesses", "emoji", "quote", "color"]
        for lang, meta in LANGUAGE_ARCHETYPES.items():
            for field in required:
                self.assertIn(field, meta, f"{lang} 缺少 {field}")

    def test_all_strengths_are_lists(self):
        """所有 strengths 都是列表"""
        for lang, meta in LANGUAGE_ARCHETYPES.items():
            self.assertIsInstance(meta["strengths"], list)

    def test_all_weaknesses_are_lists(self):
        """所有 weaknesses 都是列表"""
        for lang, meta in LANGUAGE_ARCHETYPES.items():
            self.assertIsInstance(meta["weaknesses"], list)

    def test_all_emojis_unique(self):
        """所有 emoji 唯一（不重复）"""
        emojis = [LANGUAGE_ARCHETYPES[l]["emoji"] for l in ALL_LANGUAGES]
        self.assertEqual(len(emojis), len(set(emojis)))


# ─────────────────────────────────────────────
# 时间状态计算
# ─────────────────────────────────────────────

class TestTimeBasedState(unittest.TestCase):

    def test_vitality_in_range(self):
        """精力值在 0.0~1.0 区间"""
        for h in range(24):
            v = _hour_to_vitality(h)
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_creativity_in_range(self):
        """创意值在 0.0~1.0 区间"""
        for h in range(24):
            c = _hour_to_creativity(h)
            self.assertGreaterEqual(c, 0.0)
            self.assertLessEqual(c, 1.0)

    def test_focus_in_range(self):
        """专注值在 0.0~1.0 区间"""
        for h in range(24):
            f = _hour_to_focus(h)
            self.assertGreaterEqual(f, 0.0)
            self.assertLessEqual(f, 1.0)

    def test_social_in_range(self):
        """社交值在 0.0~1.0 区间"""
        for h in range(24):
            s = _hour_to_social(h)
            self.assertGreaterEqual(s, 0.0)
            self.assertLessEqual(s, 1.0)

    def test_focus_peak_at_10am(self):
        """上午 10 点专注力应为峰值"""
        self.assertEqual(_hour_to_focus(10), 1.0)

    def test_social_peak_at_evening(self):
        """傍晚 19~20 点社交值最高"""
        self.assertGreaterEqual(_hour_to_social(19), 0.8)

    def test_calc_daily_state_returns_all_four(self):
        """四维状态全部返回"""
        state = _calc_daily_state(_FIXED_TIME)
        for key in ["精力 Vitality", "创意 Creativity", "专注 Focus", "社交 Social"]:
            self.assertIn(key, state)

    def test_mood_changes_by_hour(self):
        """不同时间段心情描述不同"""
        moods = [_time_to_mood(h) for h in range(24)]
        # 至少有几个不同的心情描述
        self.assertGreater(len(set(moods)), 5)


# ─────────────────────────────────────────────
# 运势评级
# ─────────────────────────────────────────────

class TestFortuneRating(unittest.TestCase):

    def test_fortune_returns_string(self):
        """运势返回字符串"""
        state = _calc_daily_state(_FIXED_TIME)
        f = _fortune_rating(state)
        self.assertIsInstance(f, str)

    def test_fortune_contains_emoji(self):
        """运势包含 emoji"""
        state = {"精力 Vitality": 0.8, "创意 Creativity": 0.8,
                 "专注 Focus": 0.8, "社交 Social": 0.8}
        f = _fortune_rating(state)
        self.assertTrue(any(e in f for e in ["🌟", "✨", "🌓", "🌧", "💀"]))


# ─────────────────────────────────────────────
# 条形图辅助
# ─────────────────────────────────────────────

class TestStatBar(unittest.TestCase):

    def test_bar_length(self):
        """stat bar 长度为 width"""
        bar = _build_stat_bar(0.5, width=20)
        self.assertEqual(len(bar), 20)

    def test_bar_full(self):
        """value=1.0 全为 █"""
        bar = _build_stat_bar(1.0, width=15)
        self.assertEqual(bar, "█" * 15)

    def test_bar_empty(self):
        """value=0.0 全为 ░"""
        bar = _build_stat_bar(0.0, width=15)
        self.assertEqual(bar, "░" * 15)

    def test_bar_rounds(self):
        """四舍五入正确"""
        bar = _build_stat_bar(0.67, width=10)
        self.assertIn("█", bar)
        self.assertIn("░", bar)


# ─────────────────────────────────────────────
# 属性调整
# ─────────────────────────────────────────────

class TestAttributeRating(unittest.TestCase):

    def test_adjusted_in_range(self):
        """调整后属性在 0.0~1.0 区间"""
        state = _calc_daily_state(_FIXED_TIME)
        for arch in LANGUAGE_ARCHETYPES.values():
            adjusted = _attribute_rating(state, arch["archetype"])
            for val in adjusted.values():
                self.assertGreaterEqual(val, 0.0)
                self.assertLessEqual(val, 1.0)

    def test_guardian_has_high_focus(self):
        """守护者专注调整后高于精力（专注强化）"""
        state = {"精力 Vitality": 0.7, "创意 Creativity": 0.7,
                 "专注 Focus": 0.7, "社交 Social": 0.7}
        adjusted = _attribute_rating(state, "守护者 Guardian")
        self.assertGreater(adjusted["专注 Focus"], adjusted["精力 Vitality"])

    def test_illusionist_has_high_creativity(self):
        """幻术师创意调整后高于专注（创意强化）"""
        state = {"精力 Vitality": 0.7, "创意 Creativity": 0.7,
                 "专注 Focus": 0.7, "社交 Social": 0.7}
        adjusted = _attribute_rating(state, "幻术师 Illusionist")
        self.assertGreater(adjusted["创意 Creativity"], adjusted["专注 Focus"])


# ─────────────────────────────────────────────
# ASCII 立绘
# ─────────────────────────────────────────────

class TestASCIIPortrait(unittest.TestCase):

    def test_portrait_returns_string(self):
        """立绘返回字符串"""
        p = _generate_ascii_portrait("Rust", "守护者 Guardian")
        self.assertIsInstance(p, str)

    def test_portrait_contains_emoji(self):
        """立绘包含语言 emoji"""
        p = _generate_ascii_portrait("Go", "风之精灵 Sylph")
        self.assertIn("🐹", p)

    def test_portrait_contains_archetype(self):
        """立绘包含原型名称"""
        p = _generate_ascii_portrait("JavaScript", "幻术师 Illusionist")
        self.assertIn("幻术师", p)


# ─────────────────────────────────────────────
# next_lang 轮换
# ─────────────────────────────────────────────

class TestNextLang(unittest.TestCase):

    def test_next_lang_forward(self):
        """next_lang 按顺序前进"""
        for i, lang in enumerate(ALL_LANGUAGES):
            expected = ALL_LANGUAGES[(i + 1) % len(ALL_LANGUAGES)]
            self.assertEqual(next_lang(lang), expected)

    def test_next_lang_full_cycle(self):
        """完整一圈回到起点"""
        self.assertEqual(next_lang("C/C++"), "Rust")

    def test_next_lang_unknown(self):
        """未知语言默认返回 Rust"""
        self.assertEqual(next_lang("Zig"), "Rust")


# ─────────────────────────────────────────────
# generate_archetype_report 主 API
# ─────────────────────────────────────────────

class TestGenerateArchetypeReport(unittest.TestCase):

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_generate_returns_all_fields(self):
        """返回所有字段"""
        result = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        for field in ["language", "archetype", "element", "daily_state",
                      "fortune", "report", "json_updated", "timestamp", "next_language"]:
            self.assertIn(field, result, f"缺少字段: {field}")

    def test_generate_current_language_rust(self):
        """当前语言为 Rust（index=0）"""
        result = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(result["language"], "Rust")

    def test_generate_archetype_guardian(self):
        """Rust 的原型为守护者"""
        result = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(result["archetype"], "守护者 Guardian")

    def test_generate_element(self):
        """返回元素属性"""
        result = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertIn("element", result)

    def test_generate_next_language(self):
        """下一个语言为 Go"""
        result = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(result["next_language"], "Go")

    def test_generate_updates_index(self):
        """生成后 current_index 前移一位"""
        generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 1)
        self.assertEqual(data["last_language"], "Rust")

    def test_generate_updates_timestamp(self):
        """生成后 updated_at 更新"""
        generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertNotEqual(data["updated_at"], _INITIAL_TEST_DATA["updated_at"])

    def test_generate_report_contains_language(self):
        """Markdown 报告包含语言名称"""
        result = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertIn("Rust", result["report"])

    def test_generate_report_contains_archetype(self):
        """报告包含原型名称"""
        result = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertIn("守护者", result["report"])

    def test_generate_report_contains_fortune(self):
        """报告包含运势"""
        result = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertIn("吉", result["report"])

    def test_generate_daily_state_in_range(self):
        """四维状态数值在 0.0~1.0"""
        result = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        for val in result["daily_state"].values():
            self.assertGreaterEqual(val, 0.0)
            self.assertLessEqual(val, 1.0)

    def test_generate_json_updated_true(self):
        """json_updated 为 True"""
        result = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertTrue(result["json_updated"])

    def test_full_rotation_cycle(self):
        """完整轮换一圈（8 次），验证所有语言顺序正确"""
        with open(self.test_path, "w", encoding="utf-8") as f:
            json.dump(_INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)

        for i, expected in enumerate(EXPECTED_LANGUAGES):
            result = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
            self.assertEqual(
                result["language"], expected,
                f"第 {i+1} 次轮换期望 {expected}，实际 {result['language']}"
            )


# ─────────────────────────────────────────────
# get_archetype_only
# ─────────────────────────────────────────────

class TestGetArchetypeOnly(unittest.TestCase):

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_query_does_not_change_index(self):
        """查询不推进轮换"""
        get_archetype_only(json_path=self.test_path, now=_FIXED_TIME)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 0)

    def test_query_current_language(self):
        """不指定语言时查询 Rust"""
        result = get_archetype_only(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(result["language"], "Rust")

    def test_query_specific_language_go(self):
        """指定 Go 返回 Go 的原型"""
        result = get_archetype_only(language="Go", json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(result["language"], "Go")
        self.assertEqual(result["archetype"], "风之精灵 Sylph")
        self.assertIn("domain", result)
        self.assertIn("strengths", result)
        self.assertIn("weaknesses", result)

    def test_query_all_languages(self):
        """所有语言都能查询"""
        for lang in EXPECTED_LANGUAGES:
            result = get_archetype_only(language=lang, json_path=self.test_path, now=_FIXED_TIME)
            self.assertEqual(result["language"], lang)
            self.assertIn("archetype", result)


# ─────────────────────────────────────────────
# 集成测试
# ─────────────────────────────────────────────

class TestArchetypeCanvasIntegration(unittest.TestCase):

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_consecutive_rotations(self):
        """连续轮换，索引正确前移"""
        r1 = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(r1["language"], "Rust")
        self.assertEqual(r1["next_language"], "Go")

        r2 = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(r2["language"], "Go")
        self.assertEqual(r2["next_language"], "Swift")

        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 2)

    def test_query_then_generate(self):
        """先查询不推进，再生成推进"""
        q = get_archetype_only(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(q["language"], "Rust")

        with open(self.test_path, "r", encoding="utf-8") as f:
            idx_before = json.load(f)["current_index"]

        g = generate_archetype_report(json_path=self.test_path, now=_FIXED_TIME)
        self.assertEqual(g["language"], "Rust")

        with open(self.test_path, "r", encoding="utf-8") as f:
            idx_after = json.load(f)["current_index"]

        self.assertEqual(idx_before, idx_after - 1)

    def test_different_times_different_states(self):
        """不同时间产生不同状态"""
        morning = datetime(2026, 6, 15, 10, 0, 0)  # 上午
        evening = datetime(2026, 6, 15, 20, 0, 0)   # 傍晚

        r_morning = get_archetype_only(language="Rust", json_path=self.test_path, now=morning)
        r_evening = get_archetype_only(language="Rust", json_path=self.test_path, now=evening)

        # 专注力不同（上午峰值 vs 傍晚低谷）
        self.assertNotEqual(
            r_morning["daily_state"]["专注 Focus"],
            r_evening["daily_state"]["专注 Focus"]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)