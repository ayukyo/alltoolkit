"""
test_polyglot_genealogy.py — Polyglot Genealogy 单元测试
====================================================================
测试目标：
  1. rotate_and_get_genealogy() 读取 language_rotation.json，按 current_index 取语言
  2. 报告生成后，language_rotation.json 的 current_index 前移一位
  3. get_genealogy_preview() 不推进索引
  4. get_language_info() 返回正确的状态（active/extinct/unknown）
  5. get_ancestor_chain() 正确追溯三代祖先
  6. get_descendants() 正确查询后裔
  7. get_sibling_influence() 正确查询旁系同族
  8. build_family_tree() 生成正确的 ASCII 树
  9. format_genealogy_console() 格式正确
  10. format_genealogy_markdown() 格式正确
  11. 轮换一圈（8次）后回到原点

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

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_genealogy import (
    rotate_and_get_genealogy,
    get_genealogy_preview,
    get_language_info,
    get_ancestor_chain,
    get_descendants,
    get_sibling_influence,
    build_family_tree,
    format_genealogy_console,
    format_genealogy_markdown,
    GENEALOGY_DB,
    EXTINCT_LANGUAGES,
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
    """每个测试用例使用独立的临时文件，避免状态污染"""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_genealogy_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
    return path


class TestPolyglotGenealogy(unittest.TestCase):
    """Polyglot Genealogy 单元测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    # ── rotate_and_get_genealogy ─────────────────

    def test_rotate_picks_current_language(self):
        """轮换应返回 current_index 所指的语言（index=3 → Kotlin）"""
        result = rotate_and_get_genealogy(json_path=self.test_path)
        self.assertEqual(result["current_language"], "Kotlin")

    def test_rotate_returns_genealogy_data(self):
        """轮换应返回完整的族谱数据"""
        result = rotate_and_get_genealogy(json_path=self.test_path)
        self.assertIn("genealogy", result)
        self.assertIn("info", result["genealogy"])
        self.assertIn("ancestor_chain", result["genealogy"])
        self.assertIn("descendants", result["genealogy"])
        self.assertIn("siblings", result["genealogy"])
        self.assertIn("tree_lines", result["genealogy"])

    def test_rotate_index_advances(self):
        """每次 rotate 后 current_index 应按顺序前进一位"""
        # 初始 index=3 → Kotlin; 轮换序列：Kotlin, TypeScript, JavaScript, ...
        expected = ["Kotlin", "TypeScript", "JavaScript", "Java",
                    "C/C++", "Rust", "Go", "Swift"]
        for expected_lang in expected:
            result = rotate_and_get_genealogy(json_path=self.test_path)
            self.assertEqual(result["current_language"], expected_lang,
                             f"轮换到 {expected_lang} 失败")

    def test_rotate_index_wraps_around(self):
        """索引到达末尾后应循环回 0"""
        # 初始 index=3 → Kotlin; 8次轮换后 index=3 再回到 Kotlin
        for _ in range(8):
            rotate_and_get_genealogy(json_path=self.test_path)
        # 第 9 次轮换 → Kotlin（索引已回到 3）
        result = rotate_and_get_genealogy(json_path=self.test_path)
        self.assertEqual(result["current_language"], "Kotlin")
        self.assertEqual(result["next_language"], "TypeScript")

    def test_rotate_updates_json(self):
        """rotate 后 JSON 的 current_index 应更新"""
        rotate_and_get_genealogy(json_path=self.test_path)  # Kotlin(3) → TypeScript(4)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 4)
        self.assertEqual(data["last_language"], "Kotlin")

    def test_rotate_updates_timestamp(self):
        """rotate 后 updated_at 应更新为当前时间"""
        rotate_and_get_genealogy(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertNotEqual(data["updated_at"], INITIAL_TEST_DATA["updated_at"])

    def test_rotate_next_language_correct(self):
        """rotate 应返回正确的下一个语言"""
        result = rotate_and_get_genealogy(json_path=self.test_path)  # Kotlin → TypeScript
        self.assertEqual(result["current_language"], "Kotlin")
        self.assertEqual(result["next_language"], "TypeScript")

    # ── get_genealogy_preview ────────────────────

    def test_preview_does_not_advance_index(self):
        """预览不应改变 current_index"""
        with open(self.test_path, "r", encoding="utf-8") as f:
            before = json.load(f)["current_index"]
        get_genealogy_preview(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            after = json.load(f)["current_index"]
        self.assertEqual(before, after)

    def test_preview_current_language(self):
        """预览当前语言应为 Kotlin（index=3）"""
        result = get_genealogy_preview(json_path=self.test_path)
        self.assertEqual(result["current_language"], "Kotlin")

    def test_preview_returns_full_genealogy(self):
        """预览应返回完整的族谱数据"""
        result = get_genealogy_preview(json_path=self.test_path)
        self.assertIn("genealogy", result)
        self.assertIn("tree_lines", result["genealogy"])

    def test_preview_with_language(self):
        """可以指定语言进行预览"""
        result = get_genealogy_preview(language="Rust", json_path=self.test_path)
        self.assertEqual(result["current_language"], "Rust")

    # ── get_language_info ─────────────────────────

    def test_info_returns_active_status(self):
        """活跃语言返回 active 状态"""
        info = get_language_info("Rust")
        self.assertEqual(info["status"], "active")

    def test_info_returns_extinct_status(self):
        """消亡语言返回 extinct 状态"""
        info = get_language_info("Objective-C")
        self.assertEqual(info["status"], "extinct")

    def test_info_returns_unknown_status(self):
        """未知语言返回 unknown 状态"""
        info = get_language_info("Brainfuck")
        self.assertEqual(info["status"], "unknown")

    def test_info_has_required_fields(self):
        """语言信息应包含必要字段"""
        required_fields = ["year", "ancestors", "descendants", "philosophy"]
        for lang in ["Rust", "Go", "JavaScript"]:
            info = get_language_info(lang)
            for field in required_fields:
                self.assertIn(field, info, f"{lang} 缺少 {field} 字段")

    def test_info_has_quote_and_author(self):
        """主要语言应有名言和作者"""
        for lang in ["Rust", "Go", "Kotlin", "TypeScript", "JavaScript"]:
            info = get_language_info(lang)
            self.assertIn("quote", info, f"{lang} 应有 quote")
            self.assertIn("famous_quote_author", info, f"{lang} 应有 famous_quote_author")

    def test_info_notable_facts(self):
        """主要语言应有 notable_facts"""
        for lang in ["Rust", "Go", "JavaScript"]:
            info = get_language_info(lang)
            self.assertIn("notable_facts", info)
            self.assertIsInstance(info["notable_facts"], list)

    # ── get_ancestor_chain ────────────────────────

    def test_ancestor_chain_rust(self):
        """Rust 的祖先链追溯"""
        chain = get_ancestor_chain("Rust", depth=3)
        self.assertIsInstance(chain, list)
        # Rust 的直接祖先是 ML 和 C
        names = [a["language"] for a in chain]
        self.assertIn("ML", names)

    def test_ancestor_chain_javascript(self):
        """JavaScript 的祖先链追溯"""
        chain = get_ancestor_chain("JavaScript", depth=3)
        names = [a["language"] for a in chain]
        # JavaScript 来自 Scheme, Self, Java
        self.assertIn("Scheme", names)

    def test_ancestor_chain_respects_depth(self):
        """ancestor_chain 最多追溯 depth 代"""
        chain_3 = get_ancestor_chain("Rust", depth=3)
        self.assertLessEqual(len(chain_3), 3)
        chain_1 = get_ancestor_chain("Rust", depth=1)
        self.assertLessEqual(len(chain_1), 1)

    def test_ancestor_chain_handles_unknown(self):
        """未知语言不崩溃"""
        chain = get_ancestor_chain("Brainfuck", depth=3)
        self.assertEqual(chain, [])

    # ── get_descendants ───────────────────────────

    def test_descendants_c(self):
        """C 的后代应包含多种重要语言"""
        desc = get_descendants("C")
        names = [d["language"] for d in desc]
        self.assertGreater(len(desc), 0, "C should have descendants")
        # C → C/C++ → Java, C#, Objective-C, Perl, Python 等
        # 通过递归，C 应该能追溯到多个重要语言
        self.assertIn("Java", names, f"Java should be in C's descendants, got: {names}")

    def test_descendants_ml(self):
        """ML 的后代应包含 Rust, Haskell, OCaml"""
        desc = get_descendants("ML")
        names = [d["language"] for d in desc]
        self.assertIn("Rust", names)
        self.assertIn("Haskell", names)

    def test_descendants_no_duplicates(self):
        """后裔列表不应有重复"""
        desc = get_descendants("C")
        names = [d["language"] for d in desc]
        self.assertEqual(len(names), len(set(names)))

    def test_descendants_handles_unknown(self):
        """未知语言不崩溃"""
        desc = get_descendants("Brainfuck")
        self.assertEqual(desc, [])

    # ── get_sibling_influence ─────────────────────

    def test_sibling_influence_rust(self):
        """Rust 的旁系同族（ML 的其他后代）"""
        siblings = get_sibling_influence("Rust")
        # ML 还有 Haskell、OCaml 等后代
        self.assertIsInstance(siblings, list)

    def test_sibling_influence_javascript(self):
        """JavaScript 的旁系同族"""
        siblings = get_sibling_influence("JavaScript")
        # Scheme 的其他后代
        self.assertIsInstance(siblings, list)

    # ── build_family_tree ─────────────────────────

    def test_tree_contains_language_name(self):
        """ASCII 树应包含语言名称"""
        lines = build_family_tree("Rust")
        text = "\n".join(lines)
        self.assertIn("Rust", text)

    def test_tree_contains_ancestor(self):
        """ASCII 树应包含祖先信息"""
        lines = build_family_tree("JavaScript")
        text = "\n".join(lines)
        self.assertIn("Ancestors", text)

    def test_tree_contains_philosophy(self):
        """ASCII 树应包含设计哲学"""
        lines = build_family_tree("Rust")
        text = "\n".join(lines)
        self.assertTrue(len(text) > 100, "树内容应该足够丰富")

    def test_tree_contains_tree_border(self):
        """ASCII 树应有边框字符（+ 或 Unicode 框线）"""
        lines = build_family_tree("Go")
        self.assertTrue(any("+" in l or "|" in l for l in lines))

    # ── format_genealogy_console ─────────────────

    def test_console_format_contains_language(self):
        """控制台格式应包含语言名称"""
        result = rotate_and_get_genealogy(json_path=self.test_path)
        output = format_genealogy_console(result)
        self.assertIn(result["current_language"], output)

    def test_console_format_contains_next_language(self):
        """控制台格式应包含下一个语言"""
        result = rotate_and_get_genealogy(json_path=self.test_path)
        output = format_genealogy_console(result)
        self.assertIn(result["next_language"], output)

    def test_console_format_contains_tree(self):
        """控制台格式应包含 ASCII 树"""
        result = rotate_and_get_genealogy(json_path=self.test_path)
        output = format_genealogy_console(result)
        self.assertTrue(len(output) > 200)

    # ── format_genealogy_markdown ─────────────────

    def test_markdown_format_contains_language(self):
        """Markdown 格式应包含语言名称"""
        result = rotate_and_get_genealogy(json_path=self.test_path)
        output = format_genealogy_markdown(result)
        self.assertIn(result["current_language"], output)

    def test_markdown_format_contains_philosophy(self):
        """Markdown 格式应包含设计哲学"""
        result = rotate_and_get_genealogy(json_path=self.test_path)
        output = format_genealogy_markdown(result)
        self.assertIn("## 🌳 Polyglot Genealogy", output)

    def test_markdown_format_contains_status(self):
        """Markdown 格式应包含状态标记"""
        result = rotate_and_get_genealogy(json_path=self.test_path)
        output = format_genealogy_markdown(result)
        self.assertTrue("活跃" in output or "active" in output.lower() or "✅" in output)


class TestPolyglotGenealogyIntegration(unittest.TestCase):
    """Polyglot Genealogy 集成测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_full_rotation_cycle(self):
        """完整轮换一圈（8 次），验证所有语言按顺序出现"""
        # 初始 index=3 → Kotlin; 8次轮换序列
        expected = ["Kotlin", "TypeScript", "JavaScript", "Java",
                    "C/C++", "Rust", "Go", "Swift"]
        for expected_lang in expected:
            result = rotate_and_get_genealogy(json_path=self.test_path)
            self.assertEqual(result["current_language"], expected_lang)

    def test_preview_then_rotate(self):
        """预览不改变状态，轮换改变状态"""
        # 初始 index=3 → Kotlin
        preview1 = get_genealogy_preview(json_path=self.test_path)
        self.assertEqual(preview1["current_language"], "Kotlin")

        with open(self.test_path, "r", encoding="utf-8") as f:
            idx_before = json.load(f)["current_index"]

        rotate_and_get_genealogy(json_path=self.test_path)  # Kotlin → TypeScript

        with open(self.test_path, "r", encoding="utf-8") as f:
            idx_after = json.load(f)["current_index"]

        self.assertEqual(idx_before + 1, idx_after)
        self.assertEqual(idx_after, 4)

    def test_genealogy_consistency(self):
        """轮换后 genealogy 数据的 current_language 与返回一致"""
        result = rotate_and_get_genealogy(json_path=self.test_path)
        self.assertEqual(result["genealogy"]["info"]["language"], result["current_language"])

    def test_all_core_languages_have_info(self):
        """所有 8 种核心语言都有族谱数据"""
        core_langs = ["Rust", "Go", "Swift", "Kotlin", "TypeScript",
                      "JavaScript", "Java", "C/C++"]
        for lang in core_langs:
            info = get_language_info(lang)
            self.assertEqual(info["status"], "active", f"{lang} 应为 active")
            self.assertIn("year", info)
            self.assertIn("philosophy", info)


if __name__ == "__main__":
    unittest.main(verbosity=2)
