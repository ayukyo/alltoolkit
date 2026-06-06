"""
test_polyglot_codex.py - Polyglot Codex 单元测试
====================================================================
测试目标：
  1. generate_kata() 读取 language_rotation.json，按 current_index 取语言
  2. 生成 kata 后，language_rotation.json 的 current_index 前移一位
  3. 挑战记录写入 polyglot_codex_log.json
  4. 轮换顺序正确（Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust）
  5. get_current_language() 不推进索引
  6. format_kata() 正确格式化
  7. get_codex_stats() 正确统计
  8. 所有测试通过

作者：AllToolkit 全自动生成
====================================================================
"""

import unittest
import json
import os
import sys
import tempfile
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_codex import (
    generate_kata,
    get_current_language,
    get_codex_stats,
    format_kata,
    LANGUAGE_ECOSYSTEM,
    CORE_LANGUAGES,
    _generate_fallback_kata,
)


# ─────────────────────────────────────────────
# 测试数据：8 种核心语言，current_index=0 → Rust
# ─────────────────────────────────────────────
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
    "current_index": 0,
    "last_language": "",
    "updated_at": "2026-06-06T02:10:00+08:00",
}


def _make_temp_json():
    """每个测试用例使用独立的临时文件，避免状态污染"""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_codex_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
    return path


def _make_temp_log_json():
    """创建空的挑战记录文件"""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_codex_log_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"attempts": [], "total_katas": 0}, f, ensure_ascii=False, indent=2)
    return path


# ─────────────────────────────────────────────
# 测试用例
# ─────────────────────────────────────────────

class TestPolyglotCodex(unittest.TestCase):
    """Polyglot Codex 单元测试"""

    def setUp(self):
        self.rot_path = _make_temp_json()
        self.log_path = _make_temp_log_json()

    def tearDown(self):
        for p in (self.rot_path, self.log_path):
            if os.path.exists(p):
                os.remove(p)

    # ── generate_kata：核心功能 ────────────────

    def test_kata_reads_language_from_rotation(self):
        """kata 生成应读取 current_index=0 → 语言 Rust"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(result["language"], "Rust")

    def test_kata_returns_all_required_fields(self):
        """kata 返回值应包含所有必要字段"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        required = {
            "language", "emoji", "file_ext", "paradigm",
            "theme", "difficulty", "title", "description",
            "skeleton", "test_snippet", "difficulty_stars",
            "attempt_index", "rotation_index", "next_language",
        }
        self.assertTrue(
            required.issubset(result.keys()),
            f"缺少字段：{required - result.keys()}",
        )

    def test_kata_rust_fields(self):
        """Rust kata 的元数据字段正确"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(result["emoji"], "🦀")
        self.assertEqual(result["file_ext"], "rs")
        self.assertEqual(result["paradigm"], "Systems / Memory-safe")

    def test_kata_go_fields(self):
        """Go kata 的元数据字段正确"""
        # 先把索引推进到 Go（index=1）
        rotate_once = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(rotate_once["language"], "Rust")

        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(result["language"], "Go")
        self.assertEqual(result["emoji"], "🐹")
        self.assertEqual(result["file_ext"], "go")

    def test_kata_swift_fields(self):
        """Swift kata 的元数据字段正确"""
        for _ in range(2):
            generate_kata(json_path=self.rot_path, log_path=self.log_path)
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(result["language"], "Swift")
        self.assertEqual(result["emoji"], "🦅")
        self.assertEqual(result["file_ext"], "swift")

    def test_kata_difficulty_range(self):
        """kata difficulty 应在 1-5 范围内"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertIn(result["difficulty"], range(1, 6))

    def test_kata_difficulty_stars_length(self):
        """difficulty_stars 长度应为 5"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(len(result["difficulty_stars"]), 5)

    def test_kata_description_not_empty(self):
        """kata description 不应为空"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertTrue(len(result["description"]) > 0)

    def test_kata_skeleton_not_empty(self):
        """kata skeleton 不应为空"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertTrue(len(result["skeleton"]) > 0)

    def test_kata_test_snippet_not_empty(self):
        """kata test_snippet 不应为空"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertTrue(len(result["test_snippet"]) > 0)

    def test_kata_next_language_is_correct(self):
        """Rust 的下一个语言是 Go"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(result["next_language"], "Go")

    def test_kata_rotation_index(self):
        """Rust 的 rotation_index 应为 0"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(result["rotation_index"], 0)

    # ── 轮换顺序验证 ───────────────────────────

    def test_rotation_order_rust_to_go(self):
        """Rust → Go 轮换顺序正确"""
        result1 = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(result1["language"], "Rust")

        result2 = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(result2["language"], "Go")
        self.assertEqual(result2["next_language"], "Swift")

    def test_full_rotation_cycle(self):
        """完整轮换一圈（8 次），验证所有语言按顺序出现"""
        expected = ["Rust", "Go", "Swift", "Kotlin",
                   "TypeScript", "JavaScript", "Java", "C/C++"]
        for lang in expected:
            result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
            self.assertEqual(result["language"], lang,
                             f"期望 {lang}，实际 {result['language']}")

    def test_rotation_wraps_around(self):
        """轮换到达末尾后应循环回 Rust"""
        for _ in range(8):  # 完整一圈
            generate_kata(json_path=self.rot_path, log_path=self.log_path)
        # 第 9 次 → Rust 再次出现
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(result["language"], "Rust")
        self.assertEqual(result["next_language"], "Go")

    def test_attempt_index_increments(self):
        """attempt_index 应递增"""
        r1 = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        r2 = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(r2["attempt_index"], r1["attempt_index"] + 1)

    # ── JSON 持久化 ───────────────────────────

    def test_rotation_json_index_advances(self):
        """generate_kata 后 language_rotation.json 的 current_index 应前移"""
        generate_kata(json_path=self.rot_path, log_path=self.log_path)  # Rust(0)
        with open(self.rot_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 1)

    def test_rotation_json_last_language_updated(self):
        """generate_kata 后 language_rotation.json 的 last_language 应更新"""
        generate_kata(json_path=self.rot_path, log_path=self.log_path)
        with open(self.rot_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["last_language"], "Rust")

    def test_rotation_json_updated_at_changed(self):
        """generate_kata 后 language_rotation.json 的 updated_at 应更新"""
        old_at = None
        with open(self.rot_path, "r", encoding="utf-8") as f:
            old_at = json.load(f)["updated_at"]

        generate_kata(json_path=self.rot_path, log_path=self.log_path)

        with open(self.rot_path, "r", encoding="utf-8") as f:
            new_at = json.load(f)["updated_at"]
        self.assertNotEqual(old_at, new_at)

    def test_codex_log_written(self):
        """generate_kata 后 polyglot_codex_log.json 应有记录"""
        generate_kata(json_path=self.rot_path, log_path=self.log_path)
        with open(self.log_path, "r", encoding="utf-8") as f:
            log = json.load(f)

        self.assertEqual(log["total_katas"], 1)
        self.assertEqual(len(log["attempts"]), 1)
        self.assertEqual(log["attempts"][0]["language"], "Rust")

    def test_codex_log_increments(self):
        """每次 generate_kata，total_katas 递增"""
        generate_kata(json_path=self.rot_path, log_path=self.log_path)
        generate_kata(json_path=self.rot_path, log_path=self.log_path)
        with open(self.log_path, "r", encoding="utf-8") as f:
            log = json.load(f)
        self.assertEqual(log["total_katas"], 2)
        self.assertEqual(len(log["attempts"]), 2)

    # ── get_current_language ──────────────────

    def test_current_does_not_advance_index(self):
        """get_current_language 不应改变 current_index"""
        with open(self.rot_path, "r", encoding="utf-8") as f:
            before = json.load(f)["current_index"]

        get_current_language(json_path=self.rot_path)

        with open(self.rot_path, "r", encoding="utf-8") as f:
            after = json.load(f)["current_index"]
        self.assertEqual(before, after)

    def test_current_returns_rust_at_index_zero(self):
        """current_index=0 时 get_current_language 返回 Rust"""
        st = get_current_language(json_path=self.rot_path)
        self.assertEqual(st["language"], "Rust")
        self.assertEqual(st["index"], 0)

    def test_current_after_rotate(self):
        """一次 rotate 后 get_current_language 返回 Go"""
        generate_kata(json_path=self.rot_path, log_path=self.log_path)
        st = get_current_language(json_path=self.rot_path)
        self.assertEqual(st["language"], "Go")
        self.assertEqual(st["next_language"], "Swift")

    # ── get_codex_stats ────────────────────────

    def test_stats_initial(self):
        """初始状态统计正确"""
        st = get_codex_stats(log_path=self.log_path)
        self.assertEqual(st["total_katas"], 0)
        self.assertEqual(st["per_language"], {})
        self.assertEqual(st["recent_attempts"], [])

    def test_stats_after_kata(self):
        """生成 kata 后统计正确"""
        generate_kata(json_path=self.rot_path, log_path=self.log_path)
        st = get_codex_stats(log_path=self.log_path)
        self.assertEqual(st["total_katas"], 1)
        self.assertEqual(st["per_language"]["Rust"], 1)

    def test_stats_recent_attempts(self):
        """recent_attempts 包含最近 5 次"""
        for _ in range(7):
            generate_kata(json_path=self.rot_path, log_path=self.log_path)
        st = get_codex_stats(log_path=self.log_path)
        self.assertEqual(len(st["recent_attempts"]), 5)  # 最多 5 条
        # 最后一条是最近一次（Java）
        self.assertEqual(st["recent_attempts"][-1]["language"], "Java")

    # ── format_kata ───────────────────────────

    def test_format_kata_contains_language(self):
        """format_kata 输出包含语言名称"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        formatted = format_kata(result)
        self.assertIn(result["language"], formatted)

    def test_format_kata_contains_emoji(self):
        """format_kata 输出包含 emoji"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        formatted = format_kata(result)
        self.assertIn(result["emoji"], formatted)

    def test_format_kata_contains_theme(self):
        """format_kata 输出包含主题"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        formatted = format_kata(result)
        self.assertIn(result["theme"], formatted)

    def test_format_kata_contains_skeleton(self):
        """format_kata 输出包含代码骨架"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        formatted = format_kata(result)
        # skeleton 中 {{ / }} 是 Python f-string 转义（存储为 {{ 但输出为 {）
        # 检查骨架中的关键词而非完整字符串匹配
        skeleton_text = result["skeleton"]
        self.assertTrue(
            any(keyword in formatted for keyword in ["mpsc", "thread", "fn main", "channel", "Speak", "fibonacci"]),
            f"format_kata output does not contain skeleton keywords from: {skeleton_text[:50]}",
        )

    def test_format_kata_contains_next_language(self):
        """format_kata 输出包含下一个语言"""
        result = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        formatted = format_kata(result)
        self.assertIn(result["next_language"], formatted)

    # ── _generate_fallback_kata ────────────────

    def test_fallback_kata_language_in_title(self):
        """兜底 kata 标题应包含语言名称"""
        kata = _generate_fallback_kata("Zig")
        self.assertIn("Zig", kata["title"])

    def test_fallback_kata_difficulty_one(self):
        """兜底 kata 默认难度为 1"""
        kata = _generate_fallback_kata("Zig")
        self.assertEqual(kata["difficulty"], 1)

    # ── LANGUAGE_ECOSYSTEM ─────────────────────

    def test_all_core_languages_in_ecosystem(self):
        """所有核心语言都在 LANGUAGE_ECOSYSTEM 中"""
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, LANGUAGE_ECOSYSTEM, f"{lang} not in ecosystem")

    def test_ecosystem_has_required_fields(self):
        """ecosystem 每种语言都有必要字段"""
        required = {"emoji", "file_ext", "paradigm", "kata_templates"}
        for lang in CORE_LANGUAGES:
            self.assertTrue(
                required.issubset(LANGUAGE_ECOSYSTEM[lang].keys()),
                f"{lang} 缺少字段",
            )

    def test_each_kata_has_required_fields(self):
        """每个 kata 模板都有必要字段"""
        required = {"theme", "difficulty", "title", "description", "skeleton", "test_snippet"}
        for lang in CORE_LANGUAGES:
            for kata in LANGUAGE_ECOSYSTEM[lang]["kata_templates"]:
                self.assertTrue(
                    required.issubset(kata.keys()),
                    f"{lang} kata 缺少字段：{required - kata.keys()}",
                )


class TestPolyglotCodexIntegration(unittest.TestCase):
    """Polyglot Codex 集成测试"""

    def setUp(self):
        self.rot_path = _make_temp_json()
        self.log_path = _make_temp_log_json()

    def tearDown(self):
        for p in (self.rot_path, self.log_path):
            if os.path.exists(p):
                os.remove(p)

    def test_full_workflow(self):
        """完整流程：rotate → badge → rotate → stats"""
        # 1. 生成 Rust kata
        r1 = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(r1["language"], "Rust")

        # 2. 当前语言变为 Go
        st = get_current_language(json_path=self.rot_path)
        self.assertEqual(st["language"], "Go")

        # 3. 生成 Go kata
        r2 = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(r2["language"], "Go")

        # 4. 格式化输出正确
        formatted = format_kata(r2)
        self.assertIn("Go", formatted)
        self.assertIn("🐹", formatted)

        # 5. 统计正确
        stats = get_codex_stats(log_path=self.log_path)
        self.assertEqual(stats["total_katas"], 2)
        self.assertEqual(stats["per_language"]["Rust"], 1)
        self.assertEqual(stats["per_language"]["Go"], 1)

    def test_rotation_persists_across_calls(self):
        """轮换状态在多次调用间正确保持"""
        results = []
        for _ in range(8):
            results.append(
                generate_kata(json_path=self.rot_path, log_path=self.log_path)
            )
        languages = [r["language"] for r in results]
        self.assertEqual(languages, CORE_LANGUAGES)

        # 第 9 次应该回到 Rust
        r9 = generate_kata(json_path=self.rot_path, log_path=self.log_path)
        self.assertEqual(r9["language"], "Rust")

    def test_codex_log_not_corrupted(self):
        """多次轮换后日志文件不损坏"""
        for _ in range(10):
            generate_kata(json_path=self.rot_path, log_path=self.log_path)

        with open(self.log_path, "r", encoding="utf-8") as f:
            log = json.load(f)

        self.assertEqual(log["total_katas"], 10)
        self.assertEqual(len(log["attempts"]), 10)
        # 每条记录都有必要字段
        for entry in log["attempts"]:
            self.assertIn("attempt", entry)
            self.assertIn("language", entry)
            self.assertIn("theme", entry)
            self.assertIn("title", entry)


if __name__ == "__main__":
    unittest.main(verbosity=2)